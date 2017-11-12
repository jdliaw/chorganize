//
//  ChoreViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/10/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class ChoreViewController: UIViewController {
    


    @IBAction func completechore(_ sender: Any) {
        let alert = UIAlertController(title: "Complete chore?", message: "Chore will be marked complete, but will remain on your To-Do list until removed.", preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: { _ in
            //TODO: Mark chore as completed, change background color to green.
            
            //Transition back to TabBarController
            let storyboard = UIStoryboard(name: "Main", bundle: nil)
            let TabBarVC = storyboard.instantiateViewController(withIdentifier: "TabBarController") as! UITabBarController
            let appDelegate = UIApplication.shared.delegate as! AppDelegate
            appDelegate.window?.rootViewController = TabBarVC
        }))
        alert.addAction(UIAlertAction(title: NSLocalizedString("Cancel", comment: "Cancel"), style: .cancel, handler: { _ in
            NSLog("The \"Cancel\" alert occured.")
        }))
        self.present(alert, animated: true, completion: nil)
        
    }
    @IBOutlet weak var descriptionlabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Put border around decription text.
        descriptionlabel.layer.borderWidth = 0.5
        descriptionlabel.layer.cornerRadius = 8
        
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // Send data over segue to indicate came from Edit button and set the title to "Edit Chore"
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "editChore" {
            let destVC = segue.destination as! CreateChoreViewController
            destVC.origin = "editButton"
        }
    }
}
