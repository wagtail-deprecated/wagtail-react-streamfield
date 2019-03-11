Wagtail React StreamField
=========================

.. image:: http://img.shields.io/pypi/v/wagtail-react-streamfield.svg?style=flat-square&maxAge=3600
   :target: https://pypi.python.org/pypi/wagtail-react-streamfield

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

Wagtail 2.4 or above.


Getting started
---------------

It’s really easy to setup, like most NoriPyt packages:

- ``pip install wagtail-react-streamfield``
- Add ``'wagtail_react_streamfield',`` to your ``INSTALLED_APPS``
  **before** ``'wagtail.admin'``, ``'wagtail.images'``, ``'wagtail.docs'``
  & ``'wagtail.snippets'``

That’s it!


Screenshots
-----------

.. image:: https://raw.github.com/noripyt/wagtail-react-streamfield/master/wagtail-react-streamfield-screenshot-1.png
.. image:: https://raw.github.com/noripyt/wagtail-react-streamfield/master/wagtail-react-streamfield-screenshot-2.png
.. image:: https://raw.github.com/noripyt/wagtail-react-streamfield/master/wagtail-react-streamfield-screenshot-3.png
