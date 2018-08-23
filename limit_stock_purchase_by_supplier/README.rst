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

The quantity are calculated from the purchase orders, if need return products the correct action is generate one return from the picking of the purchase order.

If the field *product variant* is set, the quantity only take this variant, but if *product variant* is empty, quantity take the field 'product' and all its variants.


Usage
=====

Create one purchase order, select the supplier and the products.

Error management
================

Los errores/fallos se gestionan en `las incidencias de GitHub <https://github.com/QubiQ/qu-purchase-workflow/issues>`_.
En caso de problemas, compruebe por favor si su incidencia ha sido ya
reportada. Si fue el primero en descubrirla, ayúdenos a solucionarla indicando
una detallada descripción `aquí <https://github.com/QubiQ/qu-purchase-workflow/issues/new>`_.


Credits
=======

Authors
~~~~~~~

* Valentin Vinagre <valentin.vinagre@qubiq.es>


Maintainer
~~~~~~~~~~

This module is maintained by QubiQ.
