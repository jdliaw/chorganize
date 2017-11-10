//
//  Chore.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/10/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class Chore {
    init?(name: String) {
        if name.isEmpty {
            return nil
        }
        self.name = name
    }
    
    var name: String
}
