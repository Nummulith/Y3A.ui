"""
AWS GUI Module

This module creates a graphical user interface (GUI) to showcase the capabilities
  of the ObjectModel Module with AWS set. It leverages the utility classes to offer
  a user-friendly interface for interacting with AWS services.

Features:
- Fetching information about objects structure in AWS cloud
- Getting AWS objects properties
- Drawing the diagram of dependencies between objects into png or svg file.

Usage:
Run the application

Author: Pavel ERESKO
"""

import importlib

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi

from Y3A import Y3A


def example(aws, module_name, function_name = None, param = None):
    """ 'Example' run """

    if function_name == None:
        function_name = module_name

    try:
        module = importlib.import_module(f"Examples." + module_name + "." + module_name)
        importlib.reload(module)

        func = getattr(module, function_name)
        func(aws, param)
                
    except Exception as e:
        print(f"Example: An exception occurred: {type(e).__name__} - {e}")


class MyWidget(QWidget):
    """ GUI Window """

    def __init__(self):
        super(MyWidget, self).__init__()
        loadUi('./Y3A.ui', self)

        self.bExample .clicked.connect(lambda: self.run_example(func = None    ))
        self.bExUpdate.clicked.connect(lambda: self.run_example(func = "update"))
        self.bExClean .clicked.connect(lambda: self.run_example(func = "clean" ))

        self.bFetch   .clicked.connect(self.fetch)
        self.bRelease .clicked.connect(self.release)
        self.bReleaseAll.clicked.connect(self.release_all)
        self.bDraw    .clicked.connect(self.draw)
        self.bReDraw  .clicked.connect(self.redraw)
        self.bDelete  .clicked.connect(self.delete)

        self.bObjectFetch.clicked.connect(self.object_fetch)
        self.bShow       .clicked.connect(self.object_show )

        self.bReset.clicked.connect(self.reset)

        self.leProfile.setText("PE")
        self.leFile   .setText("main")
        self.leClasses.setText("ALL")

        self.leExample.setText("YAML")
        self.leParam  .setText("Inter_VPC")

        self.cbAWS .setChecked(True)
        self.cbLoad.setChecked(True)

        self.y3a = None

    def get_aws(self, do_auto_load = True, do_auto_save = True):
        """ Creating the Y3A object """
        
        if self.y3a == None:
            self.y3a = Y3A(
                self.leProfile.text(),
                f"./Data/{self.leProfile.text()}_{self.leFile.text()}.xml",
                do_auto_load, do_auto_save
            )
        
        self.y3a.do_auto_load = do_auto_load
        self.y3a.do_auto_save = do_auto_save

        return self.y3a

    def reset(self):
        self.y3a = None

    def fetch(self):
        """ 'Fetch' button click """
        aws = self.get_aws(True, False)
        aws.fetch(self.leClasses.text())
        aws.save()


    def release(self):
        """ 'Release' button click """
        aws = self.get_aws(True, False)
        aws.release(self.leClasses.text())
        aws.save()

    def release_all(self):
        """ 'Release all' button click """
        aws = self.get_aws(False, False)
        aws.release("ALL")
        aws.save()


    def draw(self):
        """ 'Draw' button click """
        aws = self.get_aws(True, True)

        res = aws.html(self.leClasses.text())
        with open(f"./Data/{self.leProfile.text()}_{self.leFile.text()}.html", 'w') as file:
            file.write(res)

    def redraw(self):
        """ 'reDraw' button click """
        aws = self.get_aws(False, False)
        aws.fetch(self.leClasses.text())
        aws.save()

        self.draw()


    def delete(self):
        """ 'delete' button click """
        aws = self.get_aws()
        aws.save() #
        aws.delete_all()


    def object_fetch(self):
        """ 'fetch' button click """
        aws      = self.get_aws()
        res_type = self.leType.text()
        res_id   = self.leId.text()

        try:
            wrap = getattr(aws, res_type)
            obj = wrap.fetch(res_id)[0]

        except Exception as e:
            print(f"show: An exception occurred: {type(e).__name__} - {e}")
            return


    def object_show(self):
        """ 'show' button click """
        aws = self.get_aws()
        res_type = self.leType.text()
        res_id   = self.leId.text()

        try:
            wrap = getattr(aws, res_type)
            obj = wrap.fetch(res_id)[0]

        except Exception as e:
            print(f"show: An exception occurred: {type(e).__name__} - {e}")
            return

        print("=========")
        print(f"{res_type}::{res_id}")

        for field in [attr for attr in dir(obj)]:
            if field.startswith('__') and field.endswith('__'):
                continue
            
            value = getattr(obj, field)

            if callable(value):
                continue

            print(f"{field}: {value}")

        print("")


    def run_example(self, func = None):
        """ 'Example' button click """

        auto = self.cbLoad.isChecked()
        aws = self.get_aws(auto, auto) if self.cbAWS.isChecked() else None

        example(aws, self.leExample.text(), func, self.leParam.text())

        if aws != None and auto:
            aws.save()


if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()

def Test():
    app = QApplication([])
    wgt = MyWidget()
    wgt.draw()
