//
//  User.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/4/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class User{
    init?(name: String, email: String) {
        if name.isEmpty || email.isEmpty {
            return nil
        }
        self.name = name
        self.email = email
    }
    
    var name: String
    var email: String
}
