//
//  CreateGroupViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import Foundation
import UIKit

class CreateGroupViewController: UIViewController {
    
    @IBOutlet weak var groupName: UITextField!
    
    @IBOutlet weak var memberEmails: UITextField!
    
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
        if !email.isEmpty && groupName.text != "" && memberEmails.text != "" {
            let emailsList = memberEmails.text?.components(separatedBy: " ,")
            createGroup(email: email, groupName: groupName.text!) {
                (success: Bool) in
                var groupID: Int = 0
                getGroups(email: self.email) {
                    (groupslist: [Group]) in
                    
                    // Get groupID
                    for group in groupslist {
                        if group.name == self.groupName.text {
                            groupID = group.id
                        }
                    }
                    addUsersToGroup(groupID: groupID, listOfEmails: emailsList!) {
                        (success: Bool) in
//                        DispatchQueue.main.async {
//                            NotificationCenter.default.post(name: Notification.Name("reloadGroupTableView"), object: nil)
//                            self.dismiss()
//                        }
                        OperationQueue.main.addOperation {
                            NotificationCenter.default.post(name: NSNotification.Name(rawValue: "reloadGroupTableView"), object: nil)
                            self.dismiss()
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
