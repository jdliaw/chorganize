//
//  SecondViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class GroupViewController: UITableViewController {

    var groups = [Group]()

    override func viewDidLoad() {
        super.viewDidLoad()
        print ("in GroupViewController")
        
        // Get Email
//        var email: String = defaults.string(forKey: "email")!
        
        // Get Groups
        if let data = UserDefaults.standard.object(forKey: "groups") as? NSData {
            groups = NSKeyedUnarchiver.unarchiveObject(with: data as Data) as! [Group]
        } else {
            print ("hi")
        }
//        
//        for group in groups {
//            print (group.name)
//        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return groups.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "GroupTableViewCell", for: indexPath) as? GroupTableViewCell
        let group = groups[indexPath.row]
        
        cell!.nameLabel.text = group.name
        
        return cell!
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "groupToGroupName" {
            if let destVC = segue.destination as? GroupSplitViewController {
                let groupToPass = groups[tableView.indexPathForSelectedRow!.row]
                destVC.groupName = groupToPass.name
            }
        }
    }
    
}

