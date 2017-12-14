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
    var id: Int
    var deadlinePassed: Bool
    var groupID: Int
    
    init?(name: String, date: String, desc: String = "", id: Int, deadlinePassed: Bool = false, groupID: Int = 1) {
        if name.isEmpty || date.isEmpty {
            return nil
        }
        self.name = name
        self.date = date
        self.desc = desc
        self.id = id
        self.deadlinePassed = deadlinePassed
        self.groupID = groupID
    }
    
    required convenience init?(coder decoder: NSCoder) {
        guard let name = decoder.decodeObject(forKey: "name") as? String,
            let date = decoder.decodeObject(forKey: "date") as? String,
            let desc = decoder.decodeObject(forKey: "desc") as? String
            else { return nil }
        let id = decoder.decodeInteger(forKey: "id")
        let deadlinePassed = decoder.decodeBool(forKey: "deadlinePassed")
        let groupID = decoder.decodeInteger(forKey: "groupID")
        
        self.init(
            name: name,
            date: date,
            desc: desc,
            id: id,
            deadlinePassed: deadlinePassed,
            groupID: groupID
        )
    }
    
    func encode(with coder: NSCoder) {
        coder.encode(self.name, forKey: "name")
        coder.encode(self.date, forKey: "date")
        coder.encode(self.desc, forKey: "desc")
        coder.encode(self.id, forKey: "id")
        coder.encode(self.deadlinePassed, forKey: "deadlinePassed")
        coder.encode(self.groupID, forKey: "groupID")
    }

}
