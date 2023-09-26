#!/bin/bash

mongosh <<EOF
use admin;
db.createUser({user: "enlightai", pwd: "enlightai2023CCZ", roles:[{role: "root", db: "admin"}]});
exit;
EOF