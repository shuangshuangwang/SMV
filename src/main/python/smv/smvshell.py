#
# This file is licensed under the Apache License, Version 2.0
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
"""Helper functions available in SMV's Python shell
"""
from inspect import formatargspec, getargspec
import sys

from smv import SmvApp
from test_support.test_runner import SmvTestRunner
from test_support.testconfig import TestConfig

from pyspark.sql import DataFrame


def _jvmShellCmd():
    return SmvApp.getInstance()._jvm.org.tresamigos.smv.shell.ShellCmd

def df(name, forceRun=False, version=None, runConfig=None, quickRun=False):
    """The DataFrame result of running the named module

        Args:
            name (str): The unique name of a module. Does not have to be the FQN.
            forceRun (bool): True if the module should be forced to run even if it has persisted output. False otherwise.
            version (str): The name of the published version to load from
            runConfig (dict): runtime configuration to use when running the module
            quickRun (bool): skip computing dqm+metadata and persisting csv

        Returns:
            (DataFrame): The result of running the named module.
    """
    return SmvApp.getInstance().runModuleByName(name, forceRun, version, runConfig, quickRun)[0]

def props():
    """The current app propertied used by SMV after the app, user, command-line
        and dynamic props are merged.

        Returns:
            (dict): The 'mergedProps' or final props used by SMV
    """
    return SmvApp.getInstance().getCurrentProperties()

def dshash(name, runConfig=None):
    """The current hashOfHash for the named module as a hex string

        Args:
            name (str): The uniquen name of a module. Does not have to be the FQN.
            runConfig (dict): runConfig to apply when collecting info. If module
                              was run with a config, the same config needs to be
                              specified here to retrieve the correct hash.

        Returns:
            (int): The hashOfHash of the named module
    """
    return SmvApp.getInstance().getDsHash(name, runConfig)

def getModel(name, forceRun = False, version = None):
    """Get the result of running the named SmvModel module

        Args:
            name (str): The name of a module. Does not have to be the FQN.
            forceRun (bool): True if the module should be forced to run even if it has persisted output. False otherwise.
            version (str): The name of the published version to load from

        Returns:
            (object): The result of running the named module
    """
    app = SmvApp.getInstance()
    urn = app.inferUrn(name)
    return app.getModuleResult(urn, forceRun, version)

def openHive(tableName):
    """Read in a Hive table as a DataFrame

        Args:
            tableName (str): The name of the Hive table

        Returns:
            (DataFrame): The resulting DataFrame
    """
    return DataFrame(_jvmShellCmd().openHive(tableName), SmvApp.getInstance().sqlContext)

def openCsv(path, validate=False):
    """Read in a CSV file as a DataFrame

        Args:
            path (str): The path of the CSV file
            validate (bool): If true, validate the CSV before return DataFrame (raise error if malformatted)

        Returns:
            (DataFrame): The resulting DataFrame
    """
    app = SmvApp.getInstance()
    jdf = app.j_smvPyClient.shellOpenCsv(path, validate)
    return DataFrame(jdf, SmvApp.getInstance().sqlContext)

def smvExportCsv(name, path):
    """Export the result of a module to a CSV file at a local path

        Args:
            fqn (str): the name of the module
            path (str): a path on the local file system
    """
    _jvmShellCmd().smvExportCsv(name, path, None)

def help():
    """Print a list of the SMV helper functions available in the shell
    """
    this_mod = sys.modules[__name__]

    help_msg = "SMV shell commands:"
    for func_name in __all__:
        func = getattr(this_mod, func_name)
        signature = formatargspec(*getargspec(func))
        help_msg += "\n* {}{}".format(func_name, signature)

    smv_version = SmvApp.getInstance().j_smvApp.smvVersion()
    doc_url = ("http://tresamigossd.github.io/SMV/pythondocs/{}/smv.html#module-smv.smvshell"
                .format(smv_version))
    help_msg += "\nDocumentation may be found at " + doc_url

    print(help_msg)

def lsStage():
    """List all the stages
    """
    print(_jvmShellCmd().lsStage())

def ls(stageName = None):
    """List all datasets in a stage

        Args:
            stageName (str): The name of the stage. Defaults to None, in which ase all datasets in all stages will be listed.
    """
    if(stageName is None):
        print(_jvmShellCmd().ls())
    else:
        print(_jvmShellCmd().ls(stageName))

def lsDead(stageName = None):
    """List dead datasets in a stage

        Args:
            stageName (str): The name of the stage. Defaults to None, in which ase all datasets in all stages will be listed.
    """
    if(stageName is None):
        print(_jvmShellCmd().lsDead())
    else:
        print(_jvmShellCmd().lsDead(stageName))

def lsDeadLeaf(stageName = None):
    """List 'deadLeaf' datasets in a stage

        A 'deadLeaf' dataset is dataset for which "no modules in the stage depend
        on it, excluding Output modules"

        Note: a `deadLeaf` dataset must be `dead`, but some `dead` datasets aren't
        `leaves`.

        Args:
            stageName (str): The name of the stage. Defaults to None, in which ase all datasets in all stages will be listed.
    """
    if(stageName is None):
        print(_jvmShellCmd().lsDeadLeaf())
    else:
        print(_jvmShellCmd().lsDeadLeaf(stageName))

def exportToHive(dsname, runConfig=None):
    """Export dataset's running result to a Hive table

        Args:
            dsname (str): The name of an SmvDataSet
    """
    SmvApp.getInstance().publishModuleToHiveByName(dsname, runConfig)

def ancestors(dsname):
    """List all ancestors of a dataset

        Ancestors of a dataset are the dataset it depends on, directly or
        in-directly, including datasets from other stages.

        Args:
            dsname (str): The name of an SmvDataSet
    """
    print(_jvmShellCmd().ancestors(dsname))

def descendants(dsname):
    """List all descendants of a dataset

        Descendants of a dataset are the datasets which depend on it directly or
        in-directly, including datasets from other stages

        Args:
            dsname (str): The name of an SmvDataSet
    """
    print(_jvmShellCmd().descendants(dsname))

def graph(stageName = None):
    """Print ascii graph of all datasets in a given stage or all stages

        Args:
            stageName (str): Optional name of stage to graph. Do not
    """
    if(stageName is None):
        print(_jvmShellCmd()._graph())
    else:
        print(_jvmShellCmd()._graph(stageName))

def graphStage():
    """Print ascii graph of all stages (not datasets)
    """
    print(_jvmShellCmd()._graphStage())

def now():
    """Print current time
    """
    print(_jvmShellCmd().now())

def smvDiscoverSchemaToFile(path, n=100000, ca=None):
    """Try best to discover Schema from raw Csv file

        Will save a schema file with postfix ".toBeReviewed" in local directory.

        Args:
            path (str): Path to the CSV file
            n (int): Number of records to check for schema discovery, default 100k
            ca (CsvAttributes): Defaults to CsvWithHeader
    """
    SmvApp.getInstance()._jvm.SmvPythonHelper.smvDiscoverSchemaToFile(path, n, ca or SmvApp.getInstance().defaultCsvWithHeader())

def edd(ds_name):
    """Print edd report for the result of an SmvDataSet

        Args:
            ds_name (str): name of an SmvDataSet
    """
    report = _jvmShellCmd()._edd(ds_name)
    print(report)

def run_test(test_name):
    """Run a test with the given name without creating new Spark context

        First reloads SMV and the test from source, then runs the test.

        Args:
            test_name (str): Name of the test to run
    """
    # Ensure TestConfig has a canonical SmvApp (this will eventually be used
    # to restore the singleton SmvApp)
    TestConfig.setSmvApp(SmvApp.getInstance())

    first_dot = test_name.find(".")
    if first_dot == -1:
        test_root_name = test_name
    else:
        test_root_name = test_name[:first_dot]

    _clear_from_sys_modules(["smv", test_root_name])

    SmvTestRunner("src/test/python").run([test_name])

def _clear_from_sys_modules(names_to_clear):
    """Clear smv and the given names from sys.modules (don't clear this module)
    """
    for name in sys.modules.keys():
        for ntc in names_to_clear:
            if name != "smv.smvshell" and (name.startswith(ntc + ".") or name == ntc):
                sys.modules.pop(name)
                break

def show_run_info(collector):
    """Inspects the SmvRunInfoCollector object returned by smvApp.runModule"""
    collector.show_report()

def get_run_info(name, runConfig=None):
    """Get the SmvRunInfoCollector with full information about a module and its dependencies

        Args:
            name (str): name of the module whose information to collect
            runConfig (dict): runConfig to apply when collecting info. If module
                              was run with a config, the same config needs to be
                              specified here to retrieve the info.
    """
    return SmvApp.getInstance().getRunInfoByPartialName(name, runConfig)

__all__ = [
    'df',
    'dshash',
    'getModel',
    'openHive',
    'openCsv',
    'smvExportCsv',
    'help',
    'lsStage',
    'ls',
    'lsDead',
    'lsDeadLeaf',
    'props',
    'exportToHive',
    'ancestors',
    'descendants',
    'graph',
    'graphStage',
    'now',
    'smvDiscoverSchemaToFile',
    'edd',
    'run_test',
    'show_run_info',
    'get_run_info'
]
