Welcome to IntelliAgent's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   api/core
   api/models
   api/utils
   examples/index

Introduction
-----------

IntelliAgent is an AI agent designed to make real-time, context-aware decisions 
based on evolving data streams. By integrating advanced reasoning capabilities 
with adaptive learning, IntelliAgent continuously refines its decision-making 
processes to deliver efficient, personalized solutions.

Quick Start
----------

Installation
^^^^^^^^^^^

.. code-block:: bash

   pip install intelliagent

Basic Usage
^^^^^^^^^^

.. code-block:: python

   from intelliagent import DecisionMaker

   # Initialize the agent
   agent = DecisionMaker(
       api_key="your-api-key",
       model="gpt-4",
       domain="financial_advisor",
       continuous_learning=True
   )

   # Get decision
   decision = agent.make_decision(
       user_id="user123",
       input_data="Should I invest in tech stocks?"
   )
   print(decision)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 