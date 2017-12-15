//
//  GroupSplitViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 12/8/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class GroupSplitViewController: UIViewController {

    @IBOutlet weak var ChoresContainer: UIView!
    @IBOutlet weak var ProgressContainer: UIView!
    
    var groupName: String?
    var groupID: Int = 1
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        fetchDetails()
        self.navigationItem.title = groupName
        
        NotificationCenter.default.addObserver(self, selector: #selector(loadData), name: NSNotification.Name(rawValue: "reloadGroupSplitView"), object: nil)
    }
    
    func loadData() {
        fetchDetails()
    }
    
    func fetchDetails() {
        getGroupByID(groupID: groupID) {
            (groupName: String) in
            self.groupName = groupName
            self.navigationItem.title = groupName // Update the view's label
            OperationQueue.main.addOperation {
                self.view.setNeedsLayout()
                self.view.layoutIfNeeded()
            }
        }
    }


    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func showComponent(_ sender: UISegmentedControl) {
        if sender.selectedSegmentIndex == 0 {
            UIView.animate(withDuration: 0.5, animations: {
                self.ChoresContainer.alpha = 1
                self.ProgressContainer.alpha = 0
            })
        } else {
            UIView.animate(withDuration: 0.5, animations: {
                self.ChoresContainer.alpha = 0
                self.ProgressContainer.alpha = 1
            })
        }
    
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "editGroup" {
            if let destVC = segue.destination as? EditGroupViewController {
                destVC.groupName = self.groupName
                destVC.groupID = self.groupID
            }
        }
        
        // Pass group ID to choresByGroupTableView to load chores for appropriate group
        if segue.identifier == "choresByGroup" {
            if let destVC = segue.destination as? ChoresByGroupTableViewController {
                destVC.groupID = self.groupID
                
            }
        }
        
        // Pass group ID to ProgressView to fetch users and progress
        if segue.identifier == "groupProgress" {
            if let destVC = segue.destination as? ProgressTableViewController {
                destVC.groupID = self.groupID
            }
        }
    }
}
