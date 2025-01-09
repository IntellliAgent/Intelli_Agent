Installation
===========

Requirements
-----------

IntelliAgent requires Python 3.8 or later. The package has the following dependencies:

* openai>=1.0.0
* aiohttp>=3.8.0
* pydantic>=2.0.0

Installation Methods
------------------

Using pip
^^^^^^^^^

The easiest way to install IntelliAgent is using pip:

.. code-block:: bash

   pip install intelliagent

From Source
^^^^^^^^^^

To install IntelliAgent from source:

.. code-block:: bash

   git clone https://github.com/yourusername/intelliagent.git
   cd intelliagent
   pip install -e .

Development Installation
^^^^^^^^^^^^^^^^^^^^^^

For development, you'll want to install additional dependencies:

.. code-block:: bash

   pip install -r requirements/dev.txt

This will install all the required packages for development, including:

* Testing tools (pytest)
* Code formatting tools (black, flake8)
* Type checking tools (mypy)
* Documentation tools (sphinx) 