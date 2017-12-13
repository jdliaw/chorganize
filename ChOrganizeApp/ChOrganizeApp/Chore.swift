//
//  Chore.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/10/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit
import os.log

class Chore : NSObject, NSCoding {
    var name: String
    var date: String
    var desc: String
    
    init?(name: String, date: String, desc: String = "") {
        if name.isEmpty || date.isEmpty {
            return nil
        }
        self.name = name
        self.date = date
        self.desc = desc
    }
    
    required convenience init?(coder decoder: NSCoder) {
        guard let name = decoder.decodeObject(forKey: "name") as? String,
            let date = decoder.decodeObject(forKey: "date") as? String,
            let desc = decoder.decodeObject(forKey: "desc") as? String
            else { return nil }
        
        self.init(
            name: name,
            date: date,
            desc: desc
        )
    }
    
    func encode(with coder: NSCoder) {
        coder.encode(self.name, forKey: "name")
        coder.encode(self.date, forKey: "date")
        coder.encode(self.desc, forKey: "desc")
    }

}
