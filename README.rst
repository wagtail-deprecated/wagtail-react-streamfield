Wagtail React StreamField
=========================

.. image:: http://img.shields.io/pypi/v/wagtail-react-streamfield.svg
   :target: https://pypi.python.org/pypi/wagtail-react-streamfield
.. image:: https://img.shields.io/pypi/dm/wagtail-react-streamfield.svg
   :target: https://pypi.python.org/pypi/wagtail-react-streamfield
.. image:: https://github.com/wagtail/wagtail-react-streamfield/workflows/CI/badge.svg
   :target: https://github.com/wagtail/wagtail-react-streamfield/actions

Drop-in replacement for the StreamField in `Wagtail <https://wagtail.io/>`_.

This work was funded thanks to
`a Kickstarter campaign <https://kickstarter.com/projects/noripyt/wagtails-first-hatch>`_!

It relies on `react-streamfield <https://github.com/noripyt/react-streamfield>`_,
a React package created for the occasion.

**This work is currently in beta phase and will in the end be merged in Wagtail.**
You should be careful and manually check that it works for your own StreamField
and report any bug you find.


Requirements
------------

Wagtail 2.6 or above.


Getting started
---------------

It’s really easy to setup, like most NoriPyt packages:

- ``pip install wagtail-react-streamfield``
- Add ``'wagtail_react_streamfield',`` to your ``INSTALLED_APPS``
  **before** ``'wagtail.admin'``, ``'wagtail.images'``, ``'wagtail.docs'``
  & ``'wagtail.snippets'``

That’s it!


Usage
-----

wagtail-react-streamfield has the same class API as the regular StreamField.
What changes:

``Meta`` attributes (or passed to __init__)
...........................................

``closed``
  Set to ``True`` to close all blocks of this type when loading the page.
  Defaults to ``False``.


Screenshots
-----------

.. image:: https://raw.github.com/noripyt/wagtail-react-streamfield/master/wagtail-react-streamfield-screenshot-1.png
.. image:: https://raw.github.com/noripyt/wagtail-react-streamfield/master/wagtail-react-streamfield-screenshot-2.png
.. image:: https://raw.github.com/noripyt/wagtail-react-streamfield/master/wagtail-react-streamfield-screenshot-3.png
