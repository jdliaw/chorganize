//
//  LoginViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/8/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {

    @IBAction func moveToToDo(_ sender: AnyObject) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let TabBarVC = storyboard.instantiateViewController(withIdentifier: "TabBarController") as! UITabBarController
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        appDelegate.window?.rootViewController = TabBarVC
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}
