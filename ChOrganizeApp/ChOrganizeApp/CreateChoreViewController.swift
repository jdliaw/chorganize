//
//  CreateChoreViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 11/11/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class CreateChoreViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {
    
    // MARK: Properties
    @IBOutlet weak var groupPicker: UIPickerView!
    @IBOutlet weak var assigneePicker: UIPickerView!
    
    // Var to store data for picker
    var groupPickerData: [String] = [String]()
    var assigneePickerData: [String] = [String]()
    // default origin is the add button, optional from edit button
    var origin = ""

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Change navigation bar title based on how the user got here (using same view and logic for Create and Edit)
        if (origin == "editButton") {
            self.navigationItem.title = "Edit Chore"
        }
        
        // Connect data to picker
        self.groupPicker.delegate = self
        self.groupPicker.dataSource = self
        self.assigneePicker.delegate = self
        self.assigneePicker.dataSource = self
        
        // Input data for pickers
        groupPickerData = ["Apt 401", "Pusheen Code", "CS 130"]
        assigneePickerData = ["Isaac", "Hana", "Jenn", "Michael", "Kaitlyne", "Yanting"]
        
        groupPicker.reloadAllComponents()
        assigneePicker.reloadAllComponents()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    
    // Setting up the group UIPickerView
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    // The number of rows of data
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        if (pickerView == groupPicker) {
            return groupPickerData.count
        }
        else {
            return assigneePickerData.count
        }
    }
    
    // The data to return for the row and component (column) that's being passed in
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        if (pickerView == groupPicker) {
            return groupPickerData[row]
        }
        else {
            return assigneePickerData[row]
        }
    }

}
