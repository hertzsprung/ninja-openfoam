#!/bin/bash
sed -re 's/(.*)/\\num[round-mode=figures]{\1}/'
