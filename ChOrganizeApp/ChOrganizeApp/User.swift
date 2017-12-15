//
//  User.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class User {
    var firstName: String
    var lastName: String
    var email: String
    var progress: Int?
    
    init?(firstName: String, lastName: String, email: String) {
        
        if firstName.isEmpty || lastName.isEmpty || email.isEmpty {
            return nil
        }
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
    }
    
    func setProgress(progress: Int) {
        self.progress = progress
    }
}
