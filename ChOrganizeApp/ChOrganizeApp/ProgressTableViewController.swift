//
//  ProgressTableViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 12/8/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class ProgressTableViewController: UITableViewController {

    var members = [User]()
    var groupID: Int = 1

    override func viewDidLoad() {
        super.viewDidLoad()

        // Load progress for all users in the group
        getUsersByGroup(groupID: groupID){
            (users: [User]) in
            for user in users {
                getUserProgress(email: user.email, groupID: self.groupID) {
                    (progress: Int) in
                    user.setProgress(progress: progress)
                    self.self.members.append(user)
                    
                    // Force reload
                    OperationQueue.main.addOperation {
                        self.tableView.reloadData()
                    }
                }
            }
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source


    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return members.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ProgressTableViewCell", for: indexPath) as? ProgressTableViewCell
        let member = members[indexPath.row]

        cell!.nameLabel.text = member.firstName
        cell!.progressLabel.text = String(describing: member.progress!) + "%"
        
        return cell!
    }
}
