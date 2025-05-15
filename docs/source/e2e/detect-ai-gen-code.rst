Step-by-step: Find AI-generated code with AboutCode
========================================================


In this tutorial, we first generate code using ChatGPT, then scan the generated code in ScanCode
using the MatchCode pipeline.


- Visit chatgpt.com

- Enter this prompt to generate code:

``Write JS code that is similar to https://github.com/isaacs/inherits/``

+-----------------------------------------------------------+
|   .. image:: images/image_2.jpg                           |
|      :width: 600                                          |
+-----------------------------------------------------------+

- The results will look something like this:


+-----------------------------------------------------------+
|   .. image:: images/chatgpt_1.png                         |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  Click "Copy" button to copy the generated code then paste this in a text editor to save the
   generated code to a file named "foo.js":

+-----------------------------------------------------------+
|   .. image:: images/image_4.jpg                           |
|      :width: 600                                          |
+-----------------------------------------------------------+


- Next, open your ScanCode.io URL and click on the "New Project" button.

+-----------------------------------------------------------+
|   .. image:: images/image_3.jpg                           |
|      :width: 600                                          |
+-----------------------------------------------------------+


-  Click "Drop files over here (or click)"  and upload the saved "foo.js" file.

+-----------------------------------------------------------+
|   .. image:: images/image_5.jpg                           |
|      :width: 600                                          |
+-----------------------------------------------------------+


-  Then select the initial "scan_codebase" pipeline and click the "Create" button:

+-----------------------------------------------------------+
|   .. image:: images/image_7.jpg                           |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  Click "Add pipeline" button.

+-----------------------------------------------------------+
|   .. image:: images/image_8.jpg                           |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  Then select the "fingerprint_codebase" and cliem the "Add pipeline" button.

+-----------------------------------------------------------+
|   .. image:: images/image_9.jpg                           |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  Repeat with the "match_to_matchcode" pipeline:

+-----------------------------------------------------------+
|   .. image:: images/image_12.jpg                          |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  When the scan is done, click the "Resources" link to see the match results

+-----------------------------------------------------------+
|   .. image:: images/image_14.jpg                          |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  You can see the file was matched to the "pkg:github/isaacs/inherits@v2.0.3" PURL. This is for
   this package: https://github.com/isaacs/inherits/

+-----------------------------------------------------------+
|   .. image:: images/image_15.jpg                          |
|      :width: 600                                          |
+-----------------------------------------------------------+


-  Click on "pkg:github/isaacs/inherits@v2.0.3" package link.

+-----------------------------------------------------------+
|   .. image:: images/image_16.jpg                          |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  From there click on the "Resources" tab:

+-----------------------------------------------------------+
|   .. image:: images/image_17.jpg                          |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  Click the "foo.js" link to see the file details.

+-----------------------------------------------------------+
|   .. image:: images/image_18.jpg                          |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  Click on the "Viewer" tab to see the file content.

+-----------------------------------------------------------+
|   .. image:: images/image_19.jpg                          |
|      :width: 600                                          |
+-----------------------------------------------------------+

-  Click "Matched Snippets" sub-tab of the viewer to see the highlighted matched code:

+-----------------------------------------------------------+
|   .. image:: images/image_20.jpg                          |
|      :width: 600                                          |
+-----------------------------------------------------------+


-  The AI-generated code is highlighted as matched code below:

+-----------------------------------------------------------+
|   .. image:: images/image_21.png                          |
|      :width: 600                                          |
+-----------------------------------------------------------+


-  The matched original code is also highlighted for reference:
   https://github.com/isaacs/inherits/blob/v2.0.3/inherits_browser.js

+-----------------------------------------------------------+
|   .. image:: images/image_22.png                          |
|      :width: 600                                          |
+-----------------------------------------------------------+

