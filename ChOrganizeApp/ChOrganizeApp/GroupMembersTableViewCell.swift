//
//  GroupMembersTableViewCell.swift
//  ChOrganizeApp
//
//  Created by CLICC User on 12/14/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class GroupMembersTableViewCell: UITableViewCell {

    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var deleteButton: UIButton!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
}
