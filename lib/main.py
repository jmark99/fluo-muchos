#!/usr/bin/env python3
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from os import environ
from os import path
from sys import exit
from muchos.config import DeployConfig
from muchos.util import parse_args
import logging


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
    logging.debug("Starting main.py...")
    deploy_path = environ.get("MUCHOS_HOME")
    logging.debug(f"deploy_path:    {deploy_path}")
    if not deploy_path:
        exit("ERROR - MUCHOS_HOME env variable must be set!")
    if not path.isdir(deploy_path):
        exit(
            "ERROR - Directory set by MUCHOS_HOME does not exist: "
            + deploy_path
        )

    config_path = path.join(deploy_path, "conf/muchos.props")
    logging.debug(f"config_path:    {config_path}")
    if not path.isfile(config_path):
        exit("ERROR - A config file does not exist at " + config_path)
    checksums_path = path.join(deploy_path, "conf/checksums")
    logging.debug(f"checksums_path: {checksums_path}")

    if not path.isfile(checksums_path):
        exit("ERROR - A checksums file does not exist at " + checksums_path)

    hosts_dir = path.join(deploy_path, "conf/hosts/")
    logging.debug(f"hosts_dir:      {hosts_dir}")

    # parse command line args
    retval = parse_args(hosts_dir)
    if not retval:
        print("Invalid command line arguments. For help, use 'muchos -h'")
        exit(1)
    (opts, action, args) = retval
    logging.debug(f"opts:           {opts}")
    logging.debug(f"actions:        {action}")
    logging.debug(f"args:           {args}")

    hosts_path = path.join(hosts_dir, opts.cluster)
    logging.debug(f"hosts_path:     {hosts_path}")

    templates_path = path.join(deploy_path, "conf/templates/")
    logging.debug(f"templates_path: {templates_path}")

    config = DeployConfig(
        deploy_path,
        config_path,
        hosts_path,
        checksums_path,
        templates_path,
        opts.cluster,
    )
    config.verify_config(action)

    if action == "config":
        if opts.property == "all":
            config.print_all()
        else:
            config.print_property(opts.property)
    else:
        cluster_type = config.get("general", "cluster_type")
        logging.debug(f"cluster_type:   {cluster_type}")
        if cluster_type == "existing":
            from muchos.existing import ExistingCluster

            cluster = ExistingCluster(config)
            logging.debug(f"cluster:  {cluster.config}")
            for item in cluster.config:
                logging.debug(f"cluster: {item}")
            cluster.perform(action)
        else:
            exit("Unknown cluster_type: " + cluster_type)


main()
