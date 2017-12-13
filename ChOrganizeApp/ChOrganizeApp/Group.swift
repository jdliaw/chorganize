//
//  Group.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 11/11/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class Group : NSObject, NSCoding {
    var name: String
    var id: Int
    
    init?(name: String, id: Int) {
        if name.isEmpty {
            return nil
        }
        self.name = name
        self.id = id
    }
    
    required convenience init?(coder decoder: NSCoder) {
        guard let name = decoder.decodeObject(forKey: "name") as? String,
            let id = decoder.decodeObject(forKey: "id") as? Int
            else { return nil }
        
        self.init(
            name: name,
            id: id
        )
    }
    
    func encode(with coder: NSCoder) {
        coder.encode(self.name, forKey: "name")
        coder.encode(self.id, forKey: "id")
    }
}
