//
//  EditProfileViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 12/11/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class EditProfileViewController: UIViewController {

    @IBOutlet weak var firstNameField: UITextField!
    @IBOutlet weak var lastNameField: UITextField!
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    
    var firstName: String = ""
    var lastName: String = ""
    var email: String = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()

        firstNameField.text = firstName
        lastNameField.text = lastName
        emailField.text = email
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    @IBAction func save(_ sender: Any) {
        // Save the original user email
        let oldemail = email
        var dict = ["oldemail": oldemail] as [String : Any]
        
        if firstNameField.text != "" && firstNameField.text != firstName {
           dict["firstName"] = firstNameField.text
        }
        if lastNameField.text != "" && lastNameField.text != lastName {
            dict["lastName"] = lastNameField.text
        }
        if emailField.text != "" && emailField.text != oldemail {
            dict["newemail"] = emailField.text
        }
        if passwordField.text != "" {
            dict["password"] = passwordField.text
        }
        
        updateUser(email: oldemail, fields: dict) {
            (success: Bool) in
            if success == true {
                print("success update user")
                OperationQueue.main.addOperation {
                    NotificationCenter.default.post(name: NSNotification.Name(rawValue: "reloadProfileView"), object: nil)
                    self.dismiss()
                }
            }
            else {
                self.dismiss()
            }
        }
    }
    
    @IBAction func cancel(_ sender: Any) {
        dismiss()
    }
    
    func dismiss() {
        self.navigationController?.popViewController(animated: true)
        self.dismiss(animated: true, completion: nil)
    }
}
