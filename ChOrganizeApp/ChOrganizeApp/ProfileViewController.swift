//
//  SettingsViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class ProfileViewController: UIViewController {

    @IBOutlet weak var firstNameLabel: UILabel!
    @IBOutlet weak var lastNameLabel: UILabel!
    @IBOutlet weak var emailLabel: UILabel!
    

    var email = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        NotificationCenter.default.addObserver(self, selector: #selector(loadUser), name: NSNotification.Name(rawValue: "reloadProfileView"), object: nil)
        
        // Get email
        let defaults = UserDefaults.standard
        email = defaults.string(forKey: "email")!
        
        // Get user details
        loadUser()
    }
    
    func loadUser() {
        getUser(email: email) {
            (user: User) in
            self.firstNameLabel.text = user.firstName
            self.lastNameLabel.text = user.lastName
            self.emailLabel.text = user.email
            self.email = user.email
            
            OperationQueue.main.addOperation {
                self.view.setNeedsLayout()
            }
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func logoutAction(_ sender: Any) {
        
        // Transition back to login page
        let storyBoard : UIStoryboard = UIStoryboard(name: "Main", bundle:nil)
        
        let nextViewController = storyBoard.instantiateViewController(withIdentifier: "LoginVC") as UIViewController
        self.present(nextViewController, animated:true, completion:nil)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "profileEdit" {
            if let destVC = segue.destination as? EditProfileViewController {
                destVC.firstName = self.firstNameLabel.text!
                destVC.lastName = self.lastNameLabel.text!
                destVC.email = self.email
            }
        }
    }

}
