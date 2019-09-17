# IP Spotting

This directory contains code for identifying when an IP address belongs to a
public cloud.

The script `compile_cidrs.py` parses IP range data (in various proprietary
formats) for big cloud platforms and consolidates them into a single,
tab-delimited file called `cidrs.tsv`.

The script `check_ips.py` uses the output of the previous step, and reads in a
tab-delimited list of domains and IP addresses. It prints out a message for any
IP address that belongs to one of the cloud IP ranges discovered by the previous
step.
