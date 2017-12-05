//
//  GroupTableViewCell.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 11/11/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class GroupTableViewCell: UITableViewCell {
    
    //MARK: Properties
    @IBOutlet weak var cell: UIView!
    @IBOutlet weak var nameLabel: UILabel!
    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        
        // Configure the view for the selected state
    }
    
}
