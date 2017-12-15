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
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    @IBAction func save(_ sender: Any) {
        dismiss()
    }
    
    @IBAction func cancel(_ sender: Any) {
        dismiss()
    }
    
    func dismiss() {
        self.navigationController?.popViewController(animated: true)
        self.dismiss(animated: true, completion: nil)
    }
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
