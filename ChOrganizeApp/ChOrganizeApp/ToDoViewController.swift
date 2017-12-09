//
//  FirstViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class ToDoViewController: UITableViewController {
    
//    var chores = [Chore]()
//    var choreNameToPass = ""
//    var choreDateToPass = ""
//
//    private func loadToDoList() {
//        let chore1 = Chore(name: "Take out the trash", date: "Dec 6")
//        let chore2 = Chore(name: "Vacuum", date: "Dec 14")
//        chores.insert(chore1!, at: 0)
//        chores.insert(chore2!, at: 1)
//    }
    
    let sections = ["to-do", "completed"]
    var chores =  [[Chore]]()
    private func loadToDoList(){
        
        let chore1 = Chore(name: "Take out the trash", date: "tomorrow")
        let chore2 = Chore(name: "Vacuum", date: "yesterday")
        chores.append([Chore]())
        chores.append([Chore]())
        //groups[0].insert(group1!,at: 0)
        chores[0].append(chore1!)
        //groups[1].insert(group2!, at: 0)
        chores[1].append(chore2!)
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        loadToDoList()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // Setup tableView
    override func numberOfSections(in tableView: UITableView) -> Int {
        return 2
    }
    
    override func tableView(_ tableView:   UITableView, titleForHeaderInSection section: Int) -> String? {
        // new stuff
        return self.sections[section]
        
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return chores[section].count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ToDoTableViewCell", for: indexPath) as? ToDoTableViewCell
        let chore = chores[indexPath.section][indexPath.row]

        cell!.nameLabel.text = chore.name
        cell!.dateLabel.text = chore.date
        
//        // Save data to pass
//        choreNameToPass = chore.name
//        choreDateToPass = chore.date
//        
//        let dest : UIViewController = UIViewController() as! ChoreViewController
//        let segue : UIStoryboardSegue = UIStoryboardSegue(identifier: "choreDetail", source: self, destination: dest)
//        prepare(for: segue, sender: self)
        
        return cell!
    }
    
//    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
//        if segue.identifier == "choreDetail" {
//            let destVC = segue.destination as! ChoreViewController
//            // Pass vars
//            destVC.choreName = choreNameToPass
//            destVC.choreDate = choreDateToPass
//        }
//    }
    
}

