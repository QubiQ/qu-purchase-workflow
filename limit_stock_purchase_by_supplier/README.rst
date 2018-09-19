.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
Limit stock purchase by supplier
================================

This module allow the possibility to control the quantity of the products that we purchase to a supplier, through for range of dates and the possibility to show one message in the purchase orders.

Installation
============

Just install.


Configuration
=============

In Purchases/Purchase/Vendor Pricelists:
* Select the checkbox *Limit Purchase*.
* Date Range Limit: Select the date range wanted: monthly, quarterly, annually, custom.
* If select custom you need to insert two dates for the date range.
* Quantity:
	* The number on the left determines the purchase amount of the product in the defined date range.
	* The number on the right is the maximum of the purchase amount of the product.
* Warning in Lines: select the action to be taken when the maximum quantity is exceeded.

The quantity are calculated from the purchase invoices.

If the field *product variant* is set, the quantity only take this variant, but if *product variant* is empty, quantity take the field 'product' and all its variants.


Usage
=====

Create one purchase order, select the supplier and the products and invoice them.


Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/QubiQ/qu-purchase-workflow/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/QubiQ/qu-purchase-workflow/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.



Credits
=======

Authors
~~~~~~~

* QubiQ, Odoo Community Association (OCA)


Contributors
~~~~~~~~~~~~

* Valentin Vinagre <valentin.vinagre@qubiq.es>


Maintainer
~~~~~~~~~~

This module is maintained by QubiQ.

.. image:: https://pbs.twimg.com/profile_images/702799639855157248/ujffk9GL_200x200.png
   :alt: QubiQ
   :target: https://www.qubiq.es

This module is part of the `QubiQ/qu-purchase-workflow <https://github.com/QubiQ/qu-purchase-workflow>`_.

To contribute to this module, please visit https://github.com/QubiQ.
