//
//  Group.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 11/11/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class Group{
    init?(name: String) {
        if name.isEmpty {
            return nil
        }
        self.name = name
    }
    
    var name: String
}
