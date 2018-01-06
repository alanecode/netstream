#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Trawl Twitter's public stream and record specified network interactions.

A network is defined by: 1. a set of people (nodes) who can each be identified
by a (possibly unit) set of strings, and 2. interactions between people (edges),
for a given definition of 'interaction'.

This module can be configured to identify tweets in the public stream which
constitute evidence of an interaction between individuals in an (also
configured) set of nodes.
"""
