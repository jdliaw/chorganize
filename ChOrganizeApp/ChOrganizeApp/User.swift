//
//  User.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class User{
    var name: String
    var lastname: String
    var email: String
    
    init?(name: String, lastname: String, email: String) {
        
        if name.isEmpty || lastname.isEmpty || email.isEmpty {
            return nil
        }
        self.name = name
        self.lastname = lastname
        self.email = email
    }
}
