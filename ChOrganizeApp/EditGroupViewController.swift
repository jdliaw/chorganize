//
//  EditGroupViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class EditGroupViewController: UIViewController {

    @IBOutlet weak var descriptionField: UITextField!
    
    var groupName: String?
    var groupID: Int = 0
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.descriptionField.text = groupName
        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func cancel(_ sender: Any) {
        dismiss()
    }
    
    
    @IBAction func save(_ sender: Any) {
        dismiss()
    }
    
    @IBAction func leaveGroup(_ sender: Any) {
        let alert = UIAlertController(title: "Leave group?", message: "Are you sure you want to leave your group? Your chores will become unassigned.", preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: NSLocalizedString("Leave", comment: "Default action"), style: .`default`, handler: { _ in
            //TODO: Delete user from group
            let defaults = UserDefaults.standard
            let email: String = defaults.string(forKey: "email")!
            removeUser(groupID: self.groupID, email: email) {
                (success: Bool) in
                if success == true {
                    //Transition back to TabBarController
                    let storyboard = UIStoryboard(name: "Main", bundle: nil)
                    let TabBarVC = storyboard.instantiateViewController(withIdentifier: "TabBarController") as! UITabBarController
                    let appDelegate = UIApplication.shared.delegate as! AppDelegate
                    appDelegate.window?.rootViewController = TabBarVC
                }
            }
        }))
        alert.addAction(UIAlertAction(title: NSLocalizedString("Cancel", comment: "Cancel"), style: .cancel, handler: { _ in
            NSLog("The \"Cancel\" alert occured.")
        }))
        self.present(alert, animated: true, completion: nil)
    }

    func dismiss() {
        self.navigationController?.popViewController(animated: true)
        self.dismiss(animated: true, completion: nil)
    }

}
