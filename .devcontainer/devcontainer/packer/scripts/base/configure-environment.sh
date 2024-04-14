#!/bin/bash -e

# Add localhost alias to ::1 IPv6
# sed -i 's/::1 ip6-localhost ip6-loopback/::1     localhost ip6-localhost ip6-loopback/g' /etc/hosts

# # https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html
# # https://www.suse.com/support/kb/doc/?id=000016692
# echo 'vm.max_map_count=262144' | tee -a /etc/sysctl.conf

# # https://kind.sigs.k8s.io/docs/user/known-issues/#pod-errors-due-to-too-many-open-files
# echo 'fs.inotify.max_user_watches=655360' | tee -a /etc/sysctl.conf
# echo 'fs.inotify.max_user_instances=1280' | tee -a /etc/sysctl.conf
