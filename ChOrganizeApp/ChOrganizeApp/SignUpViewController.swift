//
//  SignUpViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class SignUpViewController: UIViewController, UITextFieldDelegate {
    
    @IBOutlet weak var firstNameField: UITextField!
    @IBOutlet weak var lastNameField: UITextField!
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    @IBOutlet weak var ScrollView: UIScrollView!
    
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        
        return true
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.emailField.delegate = self
        self.passwordField.delegate = self
        self.firstNameField.delegate = self
        self.lastNameField.delegate = self
        // Do any additional setup after loading the view.
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(LoginViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)
    }
  
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if (textField == emailField || textField == passwordField){
        ScrollView.setContentOffset(CGPoint(x:0,y:100), animated: true)
        }
        if(textField == lastNameField){
        ScrollView.setContentOffset(CGPoint(x:0,y:50), animated: true)
        }
    }
    func textFieldDidEndEditing(_ textField: UITextField) {
        if (textField == emailField || textField == passwordField || textField == lastNameField){
        
        ScrollView.setContentOffset(CGPoint(x:0,y:0), animated: true)
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    func dismissKeyboard() {
        //Causes the view (or one of its embedded text fields) to resign the first responder status.
        view.endEditing(true)
    }
    
    @IBAction func signupAction(_ sender: Any) {
        // check required fields are entered
        if firstNameField.text == "" || emailField.text == "" || passwordField.text == "" {
            signupErrorAlert(message: "One or more required fields are missing.")
        } else {
            // try to validate user
            createUser(email: emailField.text!, password: passwordField.text!, firstName: firstNameField.text!, lastName: lastNameField.text!) {
                (success: Bool) in
                if success == true {
                    OperationQueue.main.addOperation {
                        self.navigationController?.popViewController(animated: true)
                        self.dismiss(animated: true, completion: nil)
                    }
                } else {
                    OperationQueue.main.addOperation {
                        self.signupErrorAlert(message: "That email is already in use. Please enter a different email.")
                    }
                }
            }
        }
    }
    
    private func signupErrorAlert(message: String) {
        let alert = UIAlertController(
            title: "Error",
            message: message,
            preferredStyle: .alert)
        
        alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: nil))
        self.present(alert, animated: true, completion: nil)
    }

}
