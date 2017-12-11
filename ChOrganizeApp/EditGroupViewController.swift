//
//  EditGroupViewController.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class EditGroupViewController: UIViewController {

    @IBOutlet weak var descriptionField: UITextField!
    
    var groupName: String?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.descriptionField.text = groupName
        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func cancel(_ sender: Any) {
        dismiss()
    }
    
    
    @IBAction func save(_ sender: Any) {
        dismiss()
    }
    
    func dismiss() {
        self.navigationController?.popViewController(animated: true)
        self.dismiss(animated: true, completion: nil)
    }

}
