#
# Copyright (c) AboutCode.org and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://aboutcode.org for more information about AboutCode FOSSprojects.
#

import copy
import csv
import math
import os
import random
import subprocess
from collections import defaultdict

from commoncode.testcase import FileBasedTesting

from samecode import halohash

SIZE_IN_BITS = 128


def load_csv(location):
    """
    Load a CSV file at location and return a tuple of (field names, list of rows as
    mappings field->value).
    """
    with open(location) as csvin:
        reader = csv.DictReader(csvin, quoting=csv.QUOTE_NONNUMERIC)
        fields = reader.fieldnames
        values = sorted(reader, key=lambda d: d.items())
        return fields, values


def check_results(
    results,
    expected_file,
    fieldnames,
    regen=False,
):
    """
    Load and compare the CSV at `expected_file` against `results`.
    """
    if regen:
        with open(expected_file, "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows(results)

    field_names, expected = load_csv(expected_file)
    # The column name is different in the two  files
    column1_name = field_names[0]
    # check results line by line for more compact results
    for exp, res in zip(expected, results):
        assert exp[column1_name] == res[column1_name]
        expected_mean_hamming_distance = exp["mean hamming distance"]
        expected_standard_deviation = exp["standard deviation"]
        exp_min = expected_mean_hamming_distance - expected_standard_deviation
        exp_max = expected_mean_hamming_distance + expected_standard_deviation
        assert exp_min <= res["mean hamming distance"] <= exp_max


def calculate_hamming_distance(content_hash, modified_content):
    modified_content_hash = halohash.BitAverageHaloHash(modified_content)
    hamming_distance = content_hash.distance(modified_content_hash)
    return hamming_distance


def calculate_mean_and_standard_deviation(hamming_distances):
    """
    Return a tuple of the mean hamming distance value and standard deviation from
    a list of `hamming_distances`.
    """
    number_of_hamming_distances = len(hamming_distances)

    # 1: Find the mean.
    mean_hamming_distance = sum(hamming_distances) / number_of_hamming_distances

    # 2: For each data point, find the square of its distance to the mean, then sum the values.
    s0 = sum(
        (hamming_distance - mean_hamming_distance) ** 2 for hamming_distance in hamming_distances
    )

    # 3: Divide by the number of data points.
    s1 = s0 / number_of_hamming_distances

    # 4: Take the square root.
    standard_deviation = math.sqrt(s1)

    return mean_hamming_distance, standard_deviation


class TestHalohash(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), "testfiles/halohash")

    def setUp(self):
        words_loc = self.get_test_loc("words.txt")
        with open(words_loc) as f:
            self.original_content = [bytes(x.strip(), "utf-8") for x in f]

    def test_halohash_random_delete(self, regen=False):
        for number_of_words in [
            500,
        ]:
            content = copy.copy(self.original_content[:number_of_words])
            original_hash = halohash.BitAverageHaloHash(content)

            hamming_distance_by_number_of_elements = defaultdict(list)
            # Run test 40 times
            for _ in range(40):
                modified_content = copy.copy(content)
                # Do not remove more than 10% of words for this test
                # we are moving towards unrelated files past that
                n = int(math.floor(len(modified_content) * 0.10))
                for _ in range(n):
                    hamming_distance = calculate_hamming_distance(original_hash, modified_content)
                    number_of_elements = len(modified_content)
                    hamming_distance_by_number_of_elements[number_of_elements].append(
                        hamming_distance
                    )
                    modified_content.pop(random.randint(0, len(modified_content) - 1))

            # Take mean and standard deviation
            results = []
            for (
                number_of_elements,
                hamming_distances,
            ) in hamming_distance_by_number_of_elements.items():
                mean_hamming_distance, standard_deviation = calculate_mean_and_standard_deviation(
                    hamming_distances
                )
                results.append(
                    {
                        "number of hashed elements": int(number_of_elements),
                        "mean hamming distance": round(mean_hamming_distance, 1),
                        "standard deviation": round(standard_deviation, 1),
                    }
                )

            expected_results_loc = self.get_test_loc(
                f"{number_of_words}-delete-expected-results.csv"
            )
            check_results(
                results,
                expected_results_loc,
                ["number of hashed elements", "mean hamming distance", "standard deviation"],
                regen=regen,
            )

    def test_halohash_random_replace(self, regen=False):
        for number_of_words in [
            500,
        ]:
            content = copy.copy(self.original_content[:number_of_words])
            original_hash = halohash.BitAverageHaloHash(content)

            hamming_distance_by_number_of_words_replaced = defaultdict(list)

            # Run test 40 times
            for _ in range(40):
                modified_content = copy.copy(content)
                words_replaced = 0
                # Do not remove more than 10% of words for this test
                # we are moving towards unrelated files past that
                n = int(math.floor(len(modified_content) * 0.10))
                for _ in range(n):
                    hamming_distance = calculate_hamming_distance(original_hash, modified_content)
                    hamming_distance_by_number_of_words_replaced[words_replaced].append(
                        hamming_distance
                    )

                    modified_content.pop(random.randint(0, len(modified_content) - 1))
                    new_word = (
                        subprocess.run(
                            ["shuf", "-n", "1", "/usr/share/dict/american-english"],
                            stdout=subprocess.PIPE,
                        )
                        .stdout.decode("utf-8")
                        .strip()
                        .replace('"', "")
                    )
                    modified_content[random.randint(0, len(modified_content) - 1)] = bytes(
                        new_word, "utf-8"
                    )
                    words_replaced += 1

            # Take mean and standard deviation
            results = []
            for (
                words_replaced,
                hamming_distances,
            ) in hamming_distance_by_number_of_words_replaced.items():
                mean_hamming_distance, standard_deviation = calculate_mean_and_standard_deviation(
                    hamming_distances
                )
                results.append(
                    {
                        "words replaced": int(words_replaced),
                        "mean hamming distance": round(mean_hamming_distance, 1),
                        "standard deviation": round(standard_deviation, 1),
                    }
                )

            expected_results_loc = self.get_test_loc(
                f"{number_of_words}-replaced-expected-results.csv"
            )
            check_results(
                results,
                expected_results_loc,
                ["words replaced", "mean hamming distance", "standard deviation"],
                regen=regen,
            )
