//
//  EditGroupViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class EditGroupViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {

    @IBOutlet weak var descriptionField: UITextField!
    @IBOutlet weak var membersTableView: UITableView!
    
    var groupName: String?
    var groupID: Int = 0
    var members = [User]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Setup TableView for member list
        membersTableView.delegate = self
        membersTableView.dataSource = self
        
        self.descriptionField.text = groupName
        
        // Get members of group
        getUsersByGroup(groupID: groupID) {
            (users: [User]) in
            self.members = users
            // Force reload
            OperationQueue.main.addOperation {
                self.membersTableView.reloadData()
            }
        }
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
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return members.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "GroupMembersCell", for: indexPath) as? GroupMembersTableViewCell
        let member = members[indexPath.row]
        cell!.nameLabel.text = member.firstName
        
        return cell!
    }

}
