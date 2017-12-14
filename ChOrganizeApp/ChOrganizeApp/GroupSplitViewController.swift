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
        self.navigationItem.title = groupName
        // Do any additional setup after loading the view.
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
    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
