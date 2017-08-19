#!/bin/bash
sed -re 's/(.*)/\\SI{\1}{\\second}/'
