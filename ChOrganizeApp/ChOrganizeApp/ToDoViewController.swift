//
//  FirstViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class ToDoViewController: UITableViewController {
    
    let sections = ["to-do", "completed"]
    var chores =  [[Chore]]()
    var choreNameToPass = ""
    var choreDateToPass = ""
    
    private func loadToDoList(){
        let chore1 = Chore(name: "Take out the trash", date: "tomorrow")
        let chore2 = Chore(name: "Vacuum", date: "yesterday")
        chores.append([Chore]())
        chores.append([Chore]())
        chores[0].append(chore1!)
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
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "choreDetails" {
            if let destVC = segue.destination as? ChoreViewController {
                let choresToPass = chores[tableView.indexPathForSelectedRow!.section][tableView.indexPathForSelectedRow!.row]
                destVC.choreName = choresToPass.name
                destVC.choreDate = choresToPass.date
            }
        }
    }
    
}

