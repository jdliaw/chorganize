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
    @IBOutlet weak var cancelButton: UIBarButtonItem!
    @IBOutlet weak var nameLabel: UITextField!
    @IBOutlet weak var descriptionField: UITextField!
    @IBOutlet weak var deadlinePicker: UIDatePicker!
    
    // Var to store data for picker
    var groupPickerData: [String] = [String]()
    var assigneePickerData: [String] = [String]()
    
    // Var to store 2d array for assignees
    var assigneeList: [[String]] = [[String]]()
    
    // default origin is the add button, optional from edit button
    var origin = ""
    
    // Pre-filled variables for editing
    var choreName: String = ""
    var choreDate: String = ""
    var choreDescription: String = ""
    
    // Picker values
    var groupName: String = ""
    var assigneeName: String = ""
    var groupRow: Int = 0
    
    // Email 
    var email: String = ""
    var emailToPass: String = ""

    override func viewDidLoad() {
        super.viewDidLoad()
        
        let defaults = UserDefaults.standard
        email = defaults.string(forKey: "email")!

        // Change navigation bar title based on how the user got here (using same view and logic for Create and Edit)
        if (origin == "editButton") {
            self.navigationItem.title = "Edit Chore"
            self.nameLabel.text = choreName
            self.descriptionField.text = choreDescription
        }
        
        // Connect data to picker
        self.groupPicker.delegate = self
        self.groupPicker.dataSource = self
        self.assigneePicker.delegate = self
        self.assigneePicker.dataSource = self
        self.deadlinePicker.datePickerMode = UIDatePickerMode.date
        
        // Get data for pickers
        
        // Get Groups
        getGroups(email: email) {
            (groupslist: [Group]) in
            self.groupName = groupslist[0].name
            for group in groupslist {
                self.groupPickerData.append(group.name)
                
                getUsersByGroup(groupID: group.id){
                    (users: [User]) in
                    self.assigneeName = users[0].firstName
                    for user in users {
                        self.assigneePickerData.append(user.firstName)
                    }
                    OperationQueue.main.addOperation {
                        self.assigneePicker.reloadAllComponents()
                    }
                }
//                var index = 0
//                self.assigneeList.append([String]())
//                // Get Assignees
//                getUsersByGroup(groupID: group.id){
//                    (users: [User]) in
//                    for user in users {
//                        self.assigneeList[index].append(user.firstName)
//                        print ("hi")
//                        print (self.assigneeList[index])
//                    }
//                    self.assigneePickerData = self.assigneeList[0]
//                    OperationQueue.main.addOperation {
//                        self.assigneePicker.reloadAllComponents()
//                    }
//                }
//                index = index + 1
            }
            OperationQueue.main.addOperation {
                self.groupPicker.reloadAllComponents()
            }
        }
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
    
    // Value picked
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        if (pickerView == groupPicker) {
            groupName = groupPickerData[row]
        }
        else {
            assigneeName = assigneePickerData[row]
        }
    }
    
    
    // MARK: Actions

    @IBAction func cancelAction(_ sender: Any) {
        dismiss()
    }
    
    @IBAction func saveAction(_ sender: Any) {
        if nameLabel.text == "" {
            self.dismiss()
        }
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "MM/dd/yyyy"
        
        let selectedDate = dateFormatter.string(from: deadlinePicker.date)
        print(selectedDate) //send to backend
        
        print ("chorename")
        self.choreName = self.nameLabel.text ?? "failed"
        
        // Get email
        let defaults = UserDefaults.standard
        self.email = defaults.string(forKey: "email")!
        
        print("groupname")
        print(self.groupName)
        
        getGroups(email: self.email) {
            (groupslist: [Group]) in
            for group in groupslist {
                if group.name == self.groupName {
                    // Get Assignees
                    getUsersByGroup(groupID: group.id){
                        (users: [User]) in
                        for user in users {
                            if user.firstName == self.assigneeName {
                                self.emailToPass = user.email
                            }
                        }
                    }
                    // Use the group id to create the chore
                    createChore(name: self.choreName, groupID: group.id, description: self.descriptionField.text!) {
                        (choreID: Int) in
                            assignUserToChore(id: choreID, email: self.emailToPass, deadline: selectedDate) {
                                (success: Bool) in
                                if success == true {
                                    print ("success")
                                    // And we're done whew. Force the To-Do list to update.
                                    OperationQueue.main.addOperation {
                                        NotificationCenter.default.post(name: NSNotification.Name(rawValue: "loadToDoList"), object: nil)
                                        self.dismiss()
                                    }
                                }
                        }
                    }
                }
            }
        }
    }
    
    func dismiss() {
        self.navigationController?.popViewController(animated: true)
        self.dismiss(animated: true, completion: nil)
    }
    
}
