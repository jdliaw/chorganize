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
    
    private func loadGroups() {
        let group1 = Group(name: "Pusheen Code")
        let group2 = Group(name: "Apt 401")
        groups.insert(group1!,at: 0)
        groups.insert(group2!, at: 1)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        loadGroups()
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
}

