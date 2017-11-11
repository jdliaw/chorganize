//
//  FirstViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class ToDoViewController: UITableViewController {
    
    var chores = [Chore]()

    private func loadToDoList() {
        let chore1 = Chore(name: "Chore Example")
        let chore2 = Chore(name: "Chore 2")
        chores.insert(chore1!,at: 0)
        chores.insert(chore2!, at: 1)
    }
    
//    func numberOfSections(in tableView: UITableView) -> Int
//    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int
//    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell
//    
    
    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return chores.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ToDoTableViewCell", for: indexPath) as? ToDoTableViewCell
        
        let chore = chores[indexPath.row]
        
        cell!.nameLabel.text = chore.name
        
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

