#!/bin/bash
sed -re 's/(.*)/\\SI[round-mode=figures,round-precision=2]{\1}{\\meter\\per\\second}/'
