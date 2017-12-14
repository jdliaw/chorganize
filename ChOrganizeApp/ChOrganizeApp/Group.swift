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
        guard let name = decoder.decodeObject(forKey: "name") as? String
            else { return nil }
        let id = decoder.decodeInteger(forKey: "id")
        
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
