//
//  CreateGroupViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class CreateGroupViewController: UIViewController {
    
    var groupName: String = ""
    var email: String = ""

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        // Email
        let defaults = UserDefaults.standard
        email = defaults.string(forKey: "email")!
        
        //createGroup()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func cancel(_ sender: Any) {
        dismiss()
    }
    
    @IBAction func save(_ sender: Any) {
        if !email.isEmpty || !groupName.isEmpty {
            createGroup(email: email, groupName: groupName)
        }
        dismiss()
    }
    
    func dismiss() {
        self.navigationController?.popViewController(animated: true)
        self.dismiss(animated: true, completion: nil)
    }
}
