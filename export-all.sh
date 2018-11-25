#!/bin/bash
for f in ./*/; do cd $f; conan export bartoc/testing; cd ..; done

