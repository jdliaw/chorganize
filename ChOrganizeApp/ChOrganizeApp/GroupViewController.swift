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
    
    private func loadToDoList() {
        let group1 = Group(name: "Group Example")
        let group2 = Group(name: "Group 2")
        groups.insert(group1!,at: 0)
        groups.insert(group2!, at: 1)
    }
    
    //    func numberOfSections(in tableView: UITableView) -> Int
    //    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int
    //    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell
    //
    
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
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        
        loadToDoList()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
}

