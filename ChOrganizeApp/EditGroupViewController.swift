//
//  EditGroupViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class EditGroupViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {

    @IBOutlet weak var inviteMembersField: UITextField!
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
        
        print("MY GROUP: \(groupName)")
        descriptionField.text = groupName
        print(descriptionField.text)
        print("id: \(groupID)")
        
        // Get members of group
        fetchMembers()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func fetchMembers() {
        getUsersByGroup(groupID: groupID) {
            (users: [User]) in
            self.members = users
            // Force reload
            OperationQueue.main.addOperation {
                self.membersTableView.reloadData()
            }
        }
    }

    @IBAction func cancel(_ sender: Any) {
        dismiss()
    }
    
    
    @IBAction func save(_ sender: Any) {
        print("hello?")
        if descriptionField.text != "" || inviteMembersField.text != "" {
            let emailsList = inviteMembersField.text?.components(separatedBy: " ,")
            
            // Update group name
            if (descriptionField.text != "") {
                editGroupName(groupID: self.groupID, groupName: self.descriptionField.text!) {
                    (success: Bool) in
                    if success == true {
                        print("updated group name!")
                        // Add users to group
                        if self.inviteMembersField.text != "" {
                            addUsersToGroup(groupID: self.groupID, listOfEmails: emailsList!) {
                                (success: Bool) in
                                print("added users!")
                                OperationQueue.main.addOperation {
                                    NotificationCenter.default.post(name: NSNotification.Name(rawValue: "reloadGroupSplitView"), object: nil)
                                    self.dismiss()
                                }
                            }
                        }
                        else {
                            OperationQueue.main.addOperation {
                                NotificationCenter.default.post(name: NSNotification.Name(rawValue: "reloadGroupSplitView"), object: nil)
                                self.dismiss()
                            }
                        }
                    }
                    else {
                        OperationQueue.main.addOperation {
                            NotificationCenter.default.post(name: NSNotification.Name(rawValue: "reloadGroupSplitView"), object: nil)
                            self.dismiss()
                        }
                    }
                }
            }
        }
    }
    
    @IBAction func deleteMember(_ sender: Any) {
        // Manually get indexPath of row the button came from
        var indexPath: IndexPath?
        if let cell = (sender as AnyObject).superview??.superview as? GroupMembersTableViewCell {
            indexPath = membersTableView.indexPath(for: cell)
        }
        
        let alert = UIAlertController(
            title: "Delete Group Member",
            message: "Are you sure you want to remove this member?",
            preferredStyle: .alert)
        
        alert.addAction(UIAlertAction(
            title: NSLocalizedString("Delete", comment: "Default action"),
            style: .`default`,
            handler: { _ in
                let member = self.members[(indexPath?.row)!]
                removeUser(groupID: self.groupID, email: member.email) {
                    (success: Bool) in
                    if success == true {
                        // TODO: Transition back to ChoresByGroup
//                        let storyboard = UIStoryboard(name: "Main", bundle: nil)
//                        let groupChoresVC = storyboard.instantiateViewController(withIdentifier: "GroupSplitViewController")
//                        let appDelegate = UIApplication.shared.delegate as! AppDelegate
//                        appDelegate.window?.rootViewController = groupChoresVC
                        
                        // Reload data
                        self.fetchMembers()
                    }
                }
        }))
        
        alert.addAction(UIAlertAction(title: NSLocalizedString("Cancel", comment: "Cancel"), style: .cancel, handler: nil))
        
        self.present(alert, animated: true, completion: nil)
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
