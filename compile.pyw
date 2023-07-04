# -*- coding: utf-8 -*-
"""
@ File         : compile.py
@ Author       : Wcy
@ Contact      : 
@ Date         : {datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d, %H:%M:%S")}
@ Description  : compile and packeage the python projects
"""
# import windnd
from tkinter import Tk, Button, Label, Entry, StringVar, filedialog

import threading

import os
import sys
import re
import shutil
import time
from project import (Project, ProjDesc, TxtVERSION, IssScript, DescritionFileSuffix, 
                    PJ_NAME, PJ_VERSION, PJ_AUTHOR, PJ_DESCRIPTION, PJ_PATH, PJ_UUID)

ISCC_Compiler = r'C:\Users\jxyun\apps\Inno Setup 6\ISCC.exe'

def nuitka_process():
    # PyLint for Python3 thinks we import from ourselves if we really
    # import from package, pylint: disable=I0021,no-name-in-module

    # Also high complexity.
    # pylint: disable=too-many-branches,too-many-locals,too-many-statements
    if (
        os.name == "nt"
        and os.path.normcase(os.path.basename(sys.executable)) == "pythonw.exe"
    ):
        import ctypes

        ctypes.windll.user32.MessageBoxW(
            None,
            "You have to use the 'python.exe' and not a 'pythonw.exe' to run Nuitka",
            "Error",
            0x1000,  # MB_SYSTEMMODAL
        )
        sys.exit(1)

    if "NUITKA_BINARY_NAME" in os.environ:
        sys.argv[0] = os.environ["NUITKA_BINARY_NAME"]

    if "NUITKA_PYTHONPATH" in os.environ:
        # Restore the PYTHONPATH gained from the site module, that we chose not
        # to have imported during compilation. For loading ast module, we need
        # one element, that is not necessarily in our current path.
        sys.path = [os.environ["NUITKA_PYTHONPATH_AST"]]
        import ast

        sys.path = ast.literal_eval(os.environ["NUITKA_PYTHONPATH"])
        del os.environ["NUITKA_PYTHONPATH"]
    else:
        # Remove path element added for being called via "__main__.py", this can
        # only lead to trouble, having e.g. a "distutils" in sys.path that comes
        # from "nuitka.distutils".
        sys.path = [
            path_element
            for path_element in sys.path
            if os.path.dirname(os.path.abspath(__file__)) != path_element
        ]

    # We will run with the Python configuration as specified by the user, if it does
    # not match, we restart ourselves with matching configuration.
    needs_re_execution = False

    if sys.flags.no_site == 0:
        needs_re_execution = True

    # The hash randomization totally changes the created source code created,
    # changing it every single time Nuitka is run. This kills any attempt at
    # caching it, and comparing generated source code. While the created binary
    # actually may still use it, during compilation we don't want to. So lets
    # disable it.
    if os.environ.get("PYTHONHASHSEED", "-1") != "0":
        needs_re_execution = True

    # In case we need to re-execute.
    if needs_re_execution:
        from nuitka.utils.ReExecute import reExecuteNuitka  # isort:skip

        # Does not return
        reExecuteNuitka(pgo_filename=None)

    # We don't care about deprecations in any version, and these are triggered
    # by run time calculations of "range" and others, while on python2.7 they
    # are disabled by default.
    import warnings

    warnings.simplefilter("ignore", DeprecationWarning)

    from nuitka import Options  # isort:skip

    Options.parseArgs()

    Options.commentArgs()

    # Load plugins after we know, we don't execute again.
    from nuitka.plugins.Plugins import activatePlugins

    activatePlugins()

    if Options.isShowMemory():
        from nuitka.utils import MemoryUsage

        MemoryUsage.startMemoryTracing()

    if "NUITKA_NAMESPACES" in os.environ:
        # Restore the detected name space packages, that were force loaded in
        # site.py, and will need a free pass later on
        from nuitka.importing.PreloadedPackages import setPreloadedPackagePaths

        setPreloadedPackagePaths(ast.literal_eval(os.environ["NUITKA_NAMESPACES"]))
        del os.environ["NUITKA_NAMESPACES"]

    if "NUITKA_PTH_IMPORTED" in os.environ:
        # Restore the packages that the ".pth" files asked to import.
        from nuitka.importing.PreloadedPackages import setPthImportedPackages

        setPthImportedPackages(ast.literal_eval(os.environ["NUITKA_PTH_IMPORTED"]))
        del os.environ["NUITKA_PTH_IMPORTED"]

    # Now the real main program of Nuitka can take over.
    from nuitka import MainControl  # isort:skip

    MainControl.main()

    if Options.isShowMemory():
        MemoryUsage.showMemoryTrace()


def compile(proj_desc_file, version):
    project = Project()

    project.load(proj_desc_file)
    project.version = version
    project.save()

    # fixed info
    project_entry_file = 'app_main'
    project_outpath = os.path.join(project.basepath, 'out')
    project_iss_script = os.path.join(project.basepath, f'{project.name}.iss')

    project_after_compile_origin = os.path.join(project_outpath, f'{project_entry_file}.dist')
    project_after_compile_rename = os.path.join(project_outpath, f'{project.name}-{project.version}')

    # if this version need recompiled, just delete the old
    if os.path.exists(project_after_compile_rename):
        shutil.rmtree(project_after_compile_rename)

    # start compile python files with nuitka tool 
    sys.argv = [
        'nuitka',
        '--mingw64',
        '--jobs=8',
        '--standalone',
        '--disable-console',
        '--follow-imports',
        f'--windows-icon-from-ico={project.basepath}/res/ico/icon.ico',
        f'--include-data-files={project.basepath}/VERSION=VERSION',
        f'--include-data-files={project.basepath}/LICENSE=LICENSE',
        f'--include-data-dir={project.basepath}/res=res',
        '--plugin-enable=pyside6',
        f'--output-dir={project.basepath}/out/',
        '--remove-output',
        f'{project.basepath}/{project_entry_file}.py'
    ]

    # use nuitka to compile pyhton file.
    if "NUITKA_PACKAGE_HOME" in os.environ:
        sys.path.insert(0, os.environ["NUITKA_PACKAGE_HOME"])
        import nuitka  # just to have it loaded from there, pylint: disable=unused-import
        del sys.path[0]

    try:
        print("Compile:INFO: Nuitka is compiling ...")
        nuitka_process()
    except Exception as e:
        print('Compile:ERROR: %s' % e)
    else:
        time.sleep(1)
        os.rename(project_after_compile_origin, project_after_compile_rename)

    # mkdir log in destination directory
    os.mkdir(os.path.join(project_after_compile_rename, 'log'))

    # execute the inno setup
    print("Compile:INFO: Inno Setup is packaging ...")
    os.system(f'\"{ISCC_Compiler}\" {project_iss_script}')

    print("Compile:INFO: Success.")


if __name__ == '__main__':
    proj_desc_file = r'D:\Yun\Codes\Python\hellp\hellp.pyui-proj'
    version = 'beta1.0.0'

    compile(proj_desc_file, version)

   