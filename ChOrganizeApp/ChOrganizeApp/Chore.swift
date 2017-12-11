//
//  Chore.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/10/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit
import os.log

class Chore {
    init?(name: String, date: String) {
        if name.isEmpty || date.isEmpty {
            return nil
        }
        self.name = name
        self.date = date
    }
    
    var name: String
    var date: String
}
