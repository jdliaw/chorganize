//
//  ChoresByGroupTableViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class ChoresByGroupTableViewController: UITableViewController {
    
    var chores = [Chore]()
    var users = [User]()
    var groupID: Int = 1

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Get chores for the group
        getGroupChores(groupID: self.groupID) {
            (choreslist: [Chore]) in
            self.chores = choreslist
            
            for chore in choreslist {
                getUser(email: chore.userEmail) {
                    (user: User) in
                    self.users.append(user)
                    OperationQueue.main.addOperation {
                        self.tableView.reloadData()
                    }
                }
            }
            // Call to force reload
            OperationQueue.main.addOperation {
                self.tableView.reloadData()
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
        return chores.count
    }

    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ChoresByGroupTableViewCell", for: indexPath) as? ChoresByGroupTableViewCell
        let chore = chores[indexPath.row]
        
        cell!.nameLabel.text = chore.name
        cell!.dateLabel.text = chore.date
        for user in users {
            if user.email == chore.userEmail {
                cell!.personLabel.text = user.firstName
            }
        }
        return cell!
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "choreDetails" {
            if let destVC = segue.destination as? ChoreViewController {
                let choresToPass = chores[tableView.indexPathForSelectedRow!.row]
                destVC.choreName = choresToPass.name
                destVC.choreDate = choresToPass.date
                destVC.choreDescription = choresToPass.desc
            }
        }
    }
}
